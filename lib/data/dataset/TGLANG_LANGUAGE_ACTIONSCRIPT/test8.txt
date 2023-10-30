package view.scene.raid
{
    import flash.display.*;
    import flash.events.Event;
    import flash.events.MouseEvent;
    import flash.events.EventDispatcher;
    import flash.geom.*;
    import flash.filters.*;
    import flash.utils.*;
    import mx.core.*;
    import mx.controls.Label;

    import org.libspark.thread.Thread;
    import org.libspark.thread.utils.ParallelExecutor;
    import org.libspark.thread.threads.between.BeTweenAS3Thread;

    import model.*;
    import model.events.*;

    import view.image.raid.*;
    import view.*;
    import view.scene.BaseScene;
    import view.utils.*;

    import controller.RaidCtrl;


    /**
     * 渦一覧クラス
     *
     */
    public class ProfoundListContainer extends BaseScene
    {
        private static const MAP_NUM:int = 5;

        private static var __instance:ProfoundListContainer;
        private var _ctrl:RaidCtrl = RaidCtrl.instance;

        private var _profoundSceneSet:Vector.<Vector.<ProfoundScene>> = new Vector.<Vector.<ProfoundScene>>();
        private var _profoundSceneDic:Dictionary = new Dictionary();
        private var _prfPosManager:ProfoundPositionsManager = ProfoundPositionsManager.instance;


        private var _container:UIComponent = new UIComponent();

        private var _avatarId:int = 0;
        private var _mapNum:int  = 0;

        // コンテナを取る
        public static function get instance():ProfoundListContainer
        {
            if (__instance == null) __instance = new ProfoundListContainer();
            return __instance;
        }

        public static function listInitialize():void
        {
            instance.profoundSceneListClear();
            instance.profoundSceneListInit();
        }

        public static function resetImageButton(prfId:int=0):void
        {
            instance.buttonReset(prfId);
        }

        /**
         * コンストラクタ
         *
         */
        public function ProfoundListContainer()
        {
            if (Player.instance.avatar) {
                _avatarId = Player.instance.avatar.id;
            }
            addChild(_container);
        }

        // 後始末処理
        public override function final():void
        {
            profoundSceneListClear();
            RemoveChild.apply(_container);
        }

        public function listInitialize(mapNum:int=0):void
        {
            if (_profoundSceneSet.length <= 0) {
                log.writeLog(log.LV_DEBUG, this,"listInitialize",mapNum);
                for (var i:int=0;i<mapNum;i++ ) {
                    _profoundSceneSet.push(new Vector.<ProfoundScene>());
                }
                _mapNum = mapNum;
            }
            profoundSceneListClear();
            profoundSceneListInit();
        }

        // 渦の追加
        public function addProfound(prf:Profound):void
        {
            setListProfoundScene(prf,true);
        }

        // 渦の削除(非表示にする
        public function vanishProfound(prf:Profound,setViewSeq:Boolean=false):void
        {
            var prfScene:ProfoundScene = _profoundSceneDic[prf.id];
            log.writeLog(log.LV_FATAL, this,"vanishProfound",prfScene);
            if (prfScene) {
                prfScene.clickFunc = null;
                prfScene.overFunc = null;
                prfScene.outFunc = null;
                var mapId:int = (prf.questMapId != Profound.PRF_MAP_RANDOM_ID) ? prf.questMapId : prf.mapId;
                if (setViewSeq) {
                    var pExec:ParallelExecutor = new ParallelExecutor();
                    pExec.addThread(new BeTweenAS3Thread(prfScene.image, {alpha:0.0}, null, 1.0, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,false));
                    pExec.addThread(new ClousureThread(_prfPosManager.useFlagUnlock,[prf.id,mapId]));
                    pExec.start();
                } else {
                    prfScene.imageHide();
                    _prfPosManager.useFlagUnlock(prf.id,mapId);
                }
            }
        }

        // ProfoundSceneListをクリア
        private function profoundSceneListClear():void
        {
            for ( var mapId:int = 0; mapId < _mapNum; mapId++ ) {
                while (_profoundSceneSet[mapId].length > 0) {
                    var prfScene:ProfoundScene = _profoundSceneSet[mapId].pop();
                    _prfPosManager.useFlagUnlock(prfScene.profoundId,mapId);
                    prfScene = null;
                }
            }
        }

        // ProfoundSceneListの初期化
        private function profoundSceneListInit():void
        {
            for ( var mapId:int = 0; mapId < _mapNum; mapId++ ) {
                var prfList:Array = Profound.getProfoundForMapId(mapId);
                if (prfList) {
                    for ( var j:int = 0; j < prfList.length; j++ ) {
                        if (!prfList[j].isVanished) {
                            setListProfoundScene(prfList[j]);
                        } else {
                            vanishProfound(prfList[j]);
                        }
                    }
                }
            }
        }

        // ListにProfoundSceneをセット
        private function setListProfoundScene(prf:Profound,setViewSeq:Boolean=false):void
        {
            var prfScene:ProfoundScene = createProfoundScene(prf,setViewSeq);
            if (prfScene) {
                var mapId:int = (prf.questMapId != Profound.PRF_MAP_RANDOM_ID) ? prf.questMapId : prf.mapId;
                var setPos:Point = _prfPosManager.getPosPoint(prf.id,mapId,prf.posIdx);
                if (setPos) {
                    prfScene.setPosition(setPos);
                    if (_profoundSceneSet[mapId]) {
                        prfScene.clickFunc = profoundClick;
                        prfScene.overFunc = profoundMouseOver;
                        prfScene.outFunc = profoundMouseOut;
                        _container.addChild(prfScene);
                        _profoundSceneSet[mapId].push(prfScene);

                        if (setViewSeq) {
                            prfScene.imageHide();
                            var pExec:ParallelExecutor = new ParallelExecutor();
                            pExec.addThread(new BeTweenAS3Thread(prfScene.image, {alpha:1.0}, null, 1.0, BeTweenAS3Thread.EASE_OUT_SINE, 0.0 ,true));
                            pExec.start();
                        }
                    }
                }
            }
        }

        private function createProfoundScene(prf:Profound,isNew:Boolean=false):ProfoundScene
        {
            if ( _profoundSceneDic[prf.id] == null ) {
                _profoundSceneDic[prf.id] = new ProfoundScene(prf,isNew,_avatarId);
                return _profoundSceneDic[prf.id];
            } else {
                _profoundSceneDic[prf.id].profound = prf;
            }
            return _profoundSceneDic[prf.id];
        }
        private function getProfoundScene(prfId:int):ProfoundScene
        {
            return _profoundSceneDic[prfId];
        }
        private function profoundClick(prf:Profound):void
        {
            dispatchEvent(new ProfoundEvent(ProfoundEvent.SELECT, prf));
        }
        private function profoundMouseOver(prf:Profound,x:int,y:int):void
        {
            //log.writeLog(log.LV_DEBUG, this, "mouse over",prf.id,x,y);
            dispatchEvent(new ProfoundEvent(ProfoundEvent.MOUSE_OVER, prf, x, y));
        }
        private function profoundMouseOut(prf:Profound,x:int,y:int):void
        {
            //log.writeLog(log.LV_DEBUG, this, "mouse out",prf.id,x,y);
            dispatchEvent(new ProfoundEvent(ProfoundEvent.MOUSE_OUT, prf));
        }
        public function setFinish(prfId:int,finish:Boolean):void
        {
            for ( var setPrfId:Object in _profoundSceneDic) {
                if (setPrfId == prfId ) {
                    _profoundSceneDic[int(setPrfId)].finish = finish;
                }
            }
        }
        public function buttonReset(prfId:int=0):void
        {
            for ( var setPrfId:Object in _profoundSceneDic) {
                if (setPrfId == prfId ) {
                    _profoundSceneDic[int(setPrfId)].prfButtonVisible = false;
                } else {
                    _profoundSceneDic[int(setPrfId)].prfButtonVisible = true;
                }
            }
        }
        public function changeState(prfId:int=0):void
        {
            for ( var setPrfId:Object in _profoundSceneDic) {
                if (setPrfId == prfId ) {
                    _profoundSceneDic[int(setPrfId)].prfButtonVisible = false;
                } else {
                    _profoundSceneDic[int(setPrfId)].prfButtonVisible = true;
                }
            }
        }

        public function damage(prfId:int,dmg:int,strData:String,state:int,stateUpdate:Boolean):void
        {
            var prfScene:ProfoundScene = getProfoundScene(prfId);
            if (prfScene == null) return;
            prfScene.hitDamage(dmg,strData,state,stateUpdate);
        }

    }
}

